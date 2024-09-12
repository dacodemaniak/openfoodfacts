from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Sets MongoURIs
off="mongodb://admin:nimda@off-db:27017/off?directConnection=true&authSource=admin"
uptake="mongodb://uptake:27017/uptakes"
# Initialiser Spark
spark = SparkSession.builder \
    .appName("MongoDB_Extraction") \
    .config("spark.mongodb.input.uri", off) \
    .config("spark.mongodb.output.uri", uptake) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0") \
    .getOrCreate()

# Extraire les données des produits
produits_df = spark.read.format("mongo") \
    .option("database", "off") \
    .option("collection", "products") \
    .load()

# Extraire les données des mouvements de stock
mouvements_df = spark.read.format("mongo") \
    .option("database", "uptake") \
    .option("collection", "uptakes") \
    .load()

# Fusionner les dataframes
fusion_df = mouvements_df.join(produits_df, "ean", "left")

# Afficher le résultat
fusion_df.show()

# Sauvegarder le résultat dans une nouvelle collection MongoDB
fusion_df.write.format("mongo") \
    .option("database", "off") \
    .option("collection", "mouvements") \
    .mode("overwrite") \
    .save()

# Arrêter la session Spark
spark.stop()