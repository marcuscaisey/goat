/**
 * Input element which hides its error message when another character is typed.
 * If the ID of the input is "foo", then the error must have ID "foo-error".
 */
class Input {
  /**
   * @param {string} inputId - The ID of the input.
   */
  constructor(inputId) {
    document.getElementById(inputId).addEventListener("keydown", this._keydownHandler);
  }

  /**
   * Hide the error message.
   * @param {KeyboardEvent} event - Keydown event from the input.
   * @private
   */
  _keydownHandler(event) {
    let error = document.getElementById(`${event.target.id}-error`);
    if (error) {
      error.style.display = "none";
    }
  }
}

function setup() {
  new Input("id_text");
}
