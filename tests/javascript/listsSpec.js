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

  it("shouldn't hide error when no action is made", () => {
    expect(window.getComputedStyle(this.error).display).not.toBe("none");
  });

  it("should hide error on keypress", () => {
    this.input.dispatchEvent(new Event("keydown"));
    expect(window.getComputedStyle(this.error).display).toBe("none");
  });

  it("should hide error when input is clicked", () => {
    this.input.dispatchEvent(new Event("click"));
    expect(window.getComputedStyle(this.error).display).toBe("none");
  });
});
