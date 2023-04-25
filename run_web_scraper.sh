INTERACTIONS_FOLDER=mounted_volume
KWARGS=$1
REPORT_OUTPUT=$2

docker build -t web_scraper:dev -q .
mkdir $INTERACTIONS_FOLDER
cp $KWARGS $INTERACTIONS_FOLDER/kwargs.json
docker run -v $(pwd)/$INTERACTIONS_FOLDER:/service/shared --shm-size 2gb web_scraper:dev
cp $INTERACTIONS_FOLDER/report.csv $REPORT_OUTPUT
rm -rf $INTERACTIONS_FOLDER