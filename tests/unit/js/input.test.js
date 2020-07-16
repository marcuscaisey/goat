import { beforeEach, expect, it } from "@jest/globals";
import Input from "input.js";

let input, error;

beforeEach(() => {
  document.body.innerHTML = `
    <input id="input">
    <div id="input-error"></div>
  `;
  input = document.getElementById("input");
  error = document.getElementById("input-error");
  new Input("input");
});

it("shouldn't hide error when no action is made", () => {
  expect(window.getComputedStyle(error).display).not.toBe("none");
});

it("should hide error on keypress", () => {
  input.dispatchEvent(new window.KeyboardEvent("keydown"));
  expect(window.getComputedStyle(error).display).toBe("none");
});

it("should hide error when input is clicked", () => {
  input.dispatchEvent(new MouseEvent("click"));
  expect(window.getComputedStyle(error).display).toBe("none");
});
