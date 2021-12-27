package br.ufmg.dcc.lemonade.ext.fpm;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.mllib.fpm.AssociationRules;
import org.apache.spark.mllib.fpm.FPGrowth.FreqItemset;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.*;
import scala.collection.JavaConverters;
import scala.collection.Seq;
import scala.collection.mutable.WrappedArray;

import java.io.Serializable;
import java.util.List;

/**
 * Python-friendly implementation of association rules algorithm (mllib).
 * <p>
 * LemonadeAssociativeRules = spark._jvm.br.ufmg.dcc.lemonade.ext.fpm.LemonadeAssociativeRules
 * x = CustomAssociativeRules()
 * items = [[['a'], 18], [['b'], 35], [['a', 'b'], 12], [['a', 'b', 'c'], 10]]
 * df = spark.createDataFrame(items, ['rule', 'freq'])
 * df2 = x.run(spark._jsparkSession, df._jdf, 0.6)
 * <p>
 * from pyspark.sql import DataFrame
 * <p>
 * df3 = DataFrame(df2, spark)
 * df3.show()
 */
@SuppressWarnings("unused")
public class LemonadeAssociativeRules implements Serializable {

    private int itemsIndex;
    private int freqIndex;

    /**
     * Execute association rules algorithm present in Spark MLlib
     *
     * @param spark         Reference to the current Spark Session object
     * @param df            Input data frame
     * @param minConfidence Min. confidence
     * @return Data frame with rules, organized in three columns:
     * antecedent, consequent and confidence.
     */
    public Dataset<Row> run(SparkSession spark, Dataset<Row> df,
                            double minConfidence,
                            String items,
                            String freq) {

        itemsIndex = df.schema().fieldIndex(items);
        freqIndex = df.schema().fieldIndex(freq);

        JavaRDD<FreqItemset<Object>> freqItemsets = df.javaRDD().map(
                this::getFreqItemset);

        AssociationRules algorithm = new AssociationRules().setMinConfidence(
                minConfidence);

        JavaRDD<AssociationRules.Rule<Object>> rules = algorithm.run(
                freqItemsets);

        JavaRDD<Row> resultRdd = rules.map(rule ->
                RowFactory.create(getObjectSeq(rule.javaAntecedent()),
                        getObjectSeq(rule.javaConsequent()),
                        rule.confidence()));

        StructField field = df.schema().fields()[itemsIndex];
        DataType elementType = ((ArrayType) field.dataType()).elementType();

        StructType schema = new StructType()
                .add("antecedent", new ArrayType(elementType, true),
                        false, Metadata.empty())
                .add("consequent", new ArrayType(elementType, true),
                        false, Metadata.empty())
                .add("confidence", DataTypes.DoubleType);


        return spark.createDataFrame(resultRdd, schema);

    }

    private Seq<Object> getObjectSeq(List<Object> list) {
        return JavaConverters.collectionAsScalaIterableConverter(
                list).asScala().toSeq();
    }

    @SuppressWarnings("unchecked")
    private FreqItemset<Object> getFreqItemset(Row row) {
        WrappedArray<Object> itemSet = (WrappedArray<Object>) row.get(itemsIndex);

        Object[] tmpItems = new Object[itemSet.length()];
        itemSet.copyToArray(tmpItems);
        return new FreqItemset<>(tmpItems,
                ((Number) row.get(freqIndex)).longValue());
    }
}
