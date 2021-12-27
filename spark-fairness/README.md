# Fairness Metric Calculation for Spark
Calculate fairness metrics using Spark. This implementation is based on [Aequitas](http://aequitas.dssg.io/) and includes the following metrics:

- Equal Parity
- Proportional Parity
- False Positive Rate Parity
- False Discovery Rate Parity
- False Negative Rate Parity
- False Omission Rate Parity

## How to build
This project requires `sbt` (tested against version 0.13.17) and `scala` (version 2.11.x). 

```
git clone https://github.com/eubr-atmosphere/spark-fairness.git
cd spark-fairness
sbt build
```

## Spark Packages
WIP

You can use the Fairness Metric Calculation in Spark by adding its JAR file (using option `--jars`) or by using Spark Packages:
```
spark-shell --conf spark.jars.packages=spark-fairness:spark-fairness:0.1.0-spark2.1-s_2.11
```
## Usage

```FairnessEvaluatorTransformer``` is a Spark transformer, with the following parameters:

* `sensitiveColumn`: Name of the column with the sensitive information.
* `labelColumn`: Name of the column with the label information (expected result).
* `scoreColumn`: Name of the column with the score information (predicted result).
* `baselineValue`: Value used as baseline value. 
* `tau`: Define the range of assessment for the metrics.

### Python (WIP)
```python
import ...
df = spark.read.csv('samples/compas.csv')
transformer = FairnessEvaluatorTransformer(
    sensitiveColumn='race', labelColumn='label_value',
    scoreColumn='score', baselineValue='Caucasian',
    tau=0.8)
result = transformer.transform(df)
result.show()
```


