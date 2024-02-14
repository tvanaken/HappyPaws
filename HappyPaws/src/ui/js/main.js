import goodbyeWorld from "./goodbye-world.js";
import helloWorld from "./hello-world.js";

async function main() {
    console.log(helloWorld()); // eslint-disable-line no-console
    console.log(goodbyeWorld()); // eslint-disable-line no-console
}

window.onload = main; // eslint-disable-line  no-undef
