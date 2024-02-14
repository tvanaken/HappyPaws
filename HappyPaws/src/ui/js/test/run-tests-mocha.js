import assert from "assert";

import helloWorld from "../hello-world.js";

describe("Hello World Tests", () => {
    it('returns "Hello World!"', () => {
        assert.equal(helloWorld(), "Hello World!");
    });
});
