package br.ufmg.dcc.speed.lemonade.fairness

import org.apache.spark.annotation.DeveloperApi
import org.apache.spark.ml.Transformer
import org.apache.spark.ml.param._
import org.apache.spark.ml.util.Identifiable
import org.apache.spark.sql.functions.{col, count, lit, when}
import org.apache.spark.sql.types.{DataTypes, StructField, StructType}
import org.apache.spark.sql.{Column, DataFrame, Dataset}

import scala.collection.mutable.ListBuffer

private[fairness] trait FairnessEvaluatorParams extends Params {
  final val sensitiveColumn = new Param[String](
    this, "sensitiveColumn", "column with the sensitive attribute to be checked"
  )
  final val labelColumn = new Param[String](
    this, "labelColumn", "column with the label results"
  )

  final val scoreColumn = new Param[String](
    this, "scoreColumn", "column with the score results"
  )

  final val baselineValue = new Param[Any](
    this, "baselineValue", "value used as base line"
  )

  final val tau = new FloatParam(
    this, "tau", "value used to define boundaries"
  )
}

class FairnessEvaluatorTransformer(override val uid: String)
  extends Transformer with FairnessEvaluatorParams {

  def this() = this(Identifiable.randomUID("fairness"))

  override def transform(dataset: Dataset[_]): DataFrame = {
    /* Generate basic metrics */
    val totals = dataset.select(count("*").alias("total"),
      count(when(col($(scoreColumn)) === 1, 1)).alias("positives"),
      count(when(col($(scoreColumn)) === 0, 1)).alias("negatives")).first

    val aggregations = List[Column](
      (count(when(col($(labelColumn)) === 1 && col($(scoreColumn)) === 1, 1)) /
        count(when(col($(labelColumn)) === 1, 1))).alias("tpr"),

      (count(when(col($(labelColumn)) === 0 && col($(scoreColumn)) === 0, 1)) /
        count(when(col($(labelColumn)) === 0, 1))).alias("tnr"),

      (count(when(col($(labelColumn)) === 1 && col($(scoreColumn)) === 0, 1)) /
        count(when(col($(scoreColumn)) === 0, 1))).alias("for"),

      (count(when(col($(labelColumn)) === 0 && col($(scoreColumn)) === 1, 1)) /
        count(when(col($(labelColumn)) === 0, 1))).alias("fpr"),

      (count(when(col($(labelColumn)) === 1 && col($(scoreColumn)) === 0, 1)) /
        count(when(col($(labelColumn)) === 1, 1))).alias("fnr"),

      (count(when(col($(labelColumn)) === 0 && col($(scoreColumn)) === 0, 1)) /
        count(when(col($(scoreColumn)) === 0, 1))).alias("npv"),

      (count(when(col($(labelColumn)) === 1 && col($(scoreColumn)) === 1, 1)) /
        count(when(col($(scoreColumn)) === 1, 1))).alias("precision"),

      count(when(col($(scoreColumn)) === 1, 1)).alias("pp"),

      count(when(col($(scoreColumn)) === 0, 1)).alias("pn"),

      (count(when(col($(scoreColumn)) === 1, 1)) / count("*")).alias("pred_pos_ratio_g"),

      (count(when(col($(scoreColumn)) === 1, 1)) / totals.getAs[Int]("positives")).alias("pred_pos_ratio_k"),

      count(when(col($(labelColumn)) === 0 && col($(scoreColumn)) === 1, 1)).alias("fp"),
      count(when(col($(labelColumn)) === 1 && col($(scoreColumn)) === 0, 1)).alias("fn"),
      count(when(col($(labelColumn)) === 1 && col($(scoreColumn)) === 1, 1)).alias("tp"),
      count(when(col($(labelColumn)) === 0 && col($(scoreColumn)) === 0, 1)).alias("tn"),

      (count(when(col($(labelColumn)) === 0 && col($(scoreColumn)) === 1, 1)) /
        count(when(col($(scoreColumn)) === 1, 1))).alias("fdr"),

      lit(totals.getAs[Int]("positives")).alias("K"),

      count(when(col($(labelColumn)) === 1, 1)).alias("grp_label_pos"),
      count(when(col($(labelColumn)) === 0, 1)).alias("grp_label_neg"),
      count("*").alias("group_size"),
      (count(when(col($(labelColumn)) === 1, 1)) / count("*")).alias("prev")
      //lit("total_entities").alias("total_entities")
    )

    var result = dataset.groupBy(col($(sensitiveColumn))).agg(
      aggregations.head, aggregations.tail: _*).orderBy(col($(sensitiveColumn)))

    val exclude = Array($(sensitiveColumn), "total_entities", "k")

    val baselineDf = result.filter(col($(sensitiveColumn)) === $(baselineValue))
    val baselineRow = baselineDf.first
    val metricsColumns = result.schema.filter(
      f => !(exclude contains f.name))

    /* Ratio between metrics and baseline value */
    val ratios = ListBuffer[Column](col($(sensitiveColumn)), col("for"),
      col("fdr"), col("fpr"), col("fnr"), col("pred_pos_ratio_g"),
      col("pred_pos_ratio_k"), col("group_size"))

    ratios ++= metricsColumns.map(
      f => (col(f.name) / baselineRow.getAs[Double](f.name)).alias(f.name + "_disparity"))

    result = result.select(ratios: _*)

    val disparitiesColumns: Array[String] = getDisparityColumnNames

    var parities = ListBuffer[Column](
      lit(totals.getAs[Int]("total")).alias("total_records"),
      col($(sensitiveColumn)),
      lit($(sensitiveColumn)).alias("attribute"), col("for"),
      col("fdr"), col("fpr"), col("fnr"), col("pred_pos_ratio_g"),
      col("pred_pos_ratio_k"), col("group_size"))

    parities ++= result.schema.map(f => col(f.name)).to[ListBuffer]

    val inverseTau = 1.0 / $(tau)
    parities ++= disparitiesColumns.map(d => {
      (col(d) > $(tau) && col(d) < inverseTau).alias(s"${d.replace("_disparity", "")}_parity")
    }).to[ListBuffer]


    parities += (col("fdr_disparity") > $(tau) && col("fdr_disparity") < inverseTau
      && col("fpr_disparity") > $(tau) && col("fpr_disparity") < inverseTau)
      .alias("type_I_parity")

    parities += (col("for_disparity") > $(tau) && col("for_disparity") < inverseTau
      && col("fnr_disparity") > $(tau) && col("fnr_disparity") < inverseTau)
      .alias("type_II_parity")

    parities += (col("pred_pos_ratio_g_disparity") > $(tau) && col("pred_pos_ratio_g_disparity") < inverseTau
      && col("pred_pos_ratio_k_disparity") > $(tau) && col("pred_pos_ratio_k_disparity") < inverseTau)
      .alias("unsupervisioned_fairness")

    parities += (col("for_disparity") > $(tau) && col("for_disparity") < inverseTau
      && col("fnr_disparity") > $(tau) && col("fnr_disparity") < inverseTau
      && col("fdr_disparity") > $(tau) && col("fdr_disparity") < inverseTau
      && col("fpr_disparity") > $(tau) && col("fpr_disparity") < inverseTau)
      .alias("supervisioned_fairness")

    result.select(parities: _*)
  }

  private def getDisparityColumnNames: Array[String] = {
    getMainMetricColumns.map(d => s"${d}_disparity")
  }

  private def getMainMetricColumns: Array[String] = {
    Array("fnr", "for", "tnr", "pred_pos_ratio_g", "precision",
      "pred_pos_ratio_k", "fdr", "tpr", "fpr", "npv")
  }

  override def copy(extra: ParamMap): Transformer = {
    defaultCopy(extra)
  }

  @DeveloperApi
  override def transformSchema(schema: StructType): StructType = {
    val fieldNames = Array("tpr_disparity", "tnr_disparity", "for_disparity",
      "fpr_disparity", "fnr_disparity", "npv_disparity", "precision_disparity",
      "pp_disparity", "pn_disparity", "pred_pos_ratio_g_disparity",
      "pred_pos_ratio_k_disparity", "fp_disparity", "fn_disparity",
      "tp_disparity", "tn_disparity", "fdr_disparity", "grp_label_pos_disparity",
      "grp_label_neg_disparity", "group_size_disparity", "prev_disparity",

      "fnr_parity", "for_parity", "tnr_parity", "pred_pos_ratio_g_parity",
      "precision_parity", "pred_pos_ratio_k_parity", "fdr_parity",
      "tpr_parity", "fpr_parity", "npv_parity", "type_I_parity",
      "type_II_parity", "unsupervisioned_fairness", "supervisioned_fairness")
    val fields = ListBuffer(StructField($(sensitiveColumn), DataTypes.StringType,
      nullable = false),
      StructField("for", DataTypes.DoubleType,
        nullable = false),
      StructField("fdr", DataTypes.DoubleType,
        nullable = false),
      StructField("fpr", DataTypes.DoubleType,
        nullable = false),
      StructField("fnr", DataTypes.DoubleType,
        nullable = false),
      StructField("pred_pos_ratio_g", DataTypes.DoubleType,
        nullable = false),
      StructField("pred_pos_ratio_k", DataTypes.DoubleType,
        nullable = false))

    fields ++= fieldNames.map(
      f => StructField(f, DataTypes.LongType, nullable = false)).to[ListBuffer]
    StructType(fields)
  }
}

