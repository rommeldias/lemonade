name := "spark-fairness"
spName := "eubr-atmosphere/spark-fairness"
scalaVersion := "2.11.8"
sparkVersion := "2.3.0"
sparkComponents ++= Seq("mllib", "sql")
resolvers += Resolver.sonatypeRepo("public")
spShortDescription := "spark-lof"
spDescription := """A parallel implementation of fairness metrics calculation in Spark""".stripMargin
credentials += Credentials(Path.userHome / ".ivy2" / ".sbtcredentials")
licenses += "Apache-2.0" -> url("http://opensource.org/licenses/Apache-2.0")
version := "1.0"

