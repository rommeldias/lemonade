package br.ufmg.dcc.lemonade.ext.fpm;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.mllib.fpm.PrefixSpan;
import org.apache.spark.mllib.fpm.PrefixSpanModel;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.*;
import scala.collection.JavaConverters;
import scala.collection.Seq;
import scala.collection.mutable.WrappedArray;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * Python-friendly implementation of prefix span algorithm (mllib).
 */
@SuppressWarnings("unused")
public class LemonadePrefixSpan implements Serializable {

    /**
     * Execute prefix span algorithm present in Spark MLlib
     *
     * @param spark Reference to the current Spark Session object
     * @param df    Input data frame
     * @param minSupport Minimum support
     * @param maxPatternLength Maximum pattern length
     * @param items
     * @param freq
     * @return Data frame with rules, organized in two columns:
     * sequence and frequency.
     * For example, see https://pt.slideshare.net/Akanoo/prefixspan-with-spark
     */
    public Dataset<Row> run(SparkSession spark, Dataset<Row> df, float minSupport,
                            int maxPatternLength, String items, String freq) {

        JavaRDD<ArrayList<ArrayList<Object>>> sequences =
                df.javaRDD().map(this::getSequences);


        PrefixSpan prefixSpan = new PrefixSpan().setMinSupport(minSupport)
                .setMaxPatternLength(maxPatternLength);

        PrefixSpanModel<Object> model = prefixSpan.run(sequences);


        StructField field = df.schema().fields()[0];
        ArrayType arrayTypeType = (ArrayType)
                ((ArrayType) field.dataType()).elementType();

        DataType element = arrayTypeType.elementType();
        DataType elementType = ((ArrayType) field.dataType()).elementType();

        ArrayType elementSchema = new ArrayType(elementType, true);

        StructType schema = new StructType()
                .add("sequence", elementSchema,
                        false, Metadata.empty())
                .add("freq", DataTypes.LongType);

        JavaRDD<Row> resultRdd = model.freqSequences().toJavaRDD().map(
                objectFreqSequence -> RowFactory.create(
                        getObjectSeq(objectFreqSequence.javaSequence()),
                        objectFreqSequence.freq()));

        Dataset<Row> dataFrame = spark.createDataFrame(resultRdd, schema);
        dataFrame.count();
        return dataFrame;
    }

    private Seq<Object> getObjectSeq(List<List<Object>> list) {
        ArrayList<Object> result = new ArrayList<>();
        for (List<Object> row : list) {
            result.add(JavaConverters.collectionAsScalaIterableConverter(
                    row).asScala().toSeq());
        }

        return JavaConverters.collectionAsScalaIterableConverter(
                result).asScala().toSeq();
    }

    @SuppressWarnings("unchecked")
    private ArrayList<ArrayList<Object>> getSequences(Row row) {
        WrappedArray<Object> sequences = (WrappedArray<Object>) row.get(0);

        Object[] tmpItems = new Object[sequences.length()];
        sequences.copyToArray(tmpItems);

        ArrayList<ArrayList<Object>> result = new ArrayList<>();

        for (int i = 0; i < sequences.length(); i++) {
            WrappedArray<Object> seq = (WrappedArray<Object>) sequences.apply(i);
            ArrayList<Object> item = new ArrayList<>();

            for (int j = 0; j < seq.length(); j++) {
                item.add(seq.apply(j));
            }
            result.add(item);
        }
        return result;
    }
}
