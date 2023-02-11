import { assertEquals } from "https://deno.land/std@0.174.0/testing/asserts.ts";
import { describe, it } from "https://deno.land/std@0.174.0/testing/bdd.ts";

import { greet } from "../mod.ts";

describe("example", () => {
  it("greet", () => {
    assertEquals(greet('World'), 'Hello World');
  });
});