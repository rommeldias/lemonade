package br.ufmg.dcc.lemonade.ext.fpm;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

/**
 * Extension to calculate metrics from two data frames: one containing frequent
 * item sets and other containing the generated rules.
 */
public class MetricCalculator {
    public void run(SparkSession spark, Dataset<Row> freqItems,
                    Dataset<Row> rules) {


    }
}
