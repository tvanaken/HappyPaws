// EDIT THIS FILE TO COMPLETE ASSIGNMENT QUESTION 1
const { chromium } = require("playwright");

async function sortHackerNewsArticles() {
    // launch browser
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    // go to Hacker News
    await page.goto("https://news.ycombinator.com/newest");

    let timestamps = [];
    let count = 0;

    while (timestamps.length < 100) {
        const age = page.locator(".age");

        const pageTimestamps = await age.evaluateAll((elements) => {
            return elements
                .slice(0, 100)
                .map((element) => element.getAttribute("title"));
        });

        timestamps = timestamps.concat(
            pageTimestamps.slice(0, 100 - timestamps.length)
        );

        count = timestamps.length;
        console.log(count + " Article dates pulled");

        if (timestamps.length >= 100) break;

        const moreButton = page.locator(".morelink");
        await moreButton.click();

        await page.waitForLoadState("networkidle");
    }

    const dates = timestamps.map((timestamp) => new Date(timestamp));
    let isSorted = true;
    for (let i = 0; i < dates.length - 1; i++) {
        if (dates[i] < dates[i + 1]) {
            isSorted = false;
            break;
        }
    }

    if (isSorted) {
        console.log("The list of articles is sorted from newest to oldest");
    } else {
        console.log("The list is not sorted correctly");
    }

    await browser.close();
}

(async () => {
    await sortHackerNewsArticles();
})();
