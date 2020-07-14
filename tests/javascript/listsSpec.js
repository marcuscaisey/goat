describe("Input", () => {
  beforeEach(() => {
    this.input = document.createElement("input");
    this.input.id = "input";
    this.error = document.createElement("div");
    this.error.id = "input-error";
    document.body.appendChild(this.input);
    document.body.appendChild(this.error)
    new Input("input");
  });

  afterEach(() => {
    this.input.remove();
    this.error.remove();
  });

  it("should hide error on keypress", () => {
    this.input.dispatchEvent(new Event("keydown"));
    expect(window.getComputedStyle(this.error).display).toBe("none");
  });

  it("shouldn't hide error without keypress", () => {
    expect(window.getComputedStyle(this.error).display).not.toBe("none");
  });
});
