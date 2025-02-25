const { crawlData } = require('./DataScraping');

const startDate = process.argv[2];
const endDate = process.argv[3];

(async () => {
    const data = await crawlData(startDate, endDate);
    console.log(JSON.stringify(data));
})();