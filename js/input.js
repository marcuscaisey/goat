/**
 * Input element which hides its error message when another character is typed
 * or it gets clicked. If the ID of the input is "foo", then the error must have
 * ID "foo-error".
 */
export default class Input {
  /**
   * @param {string} inputId - The ID of the input.
   */
  constructor(inputId) {
    let input = document.getElementById(inputId);
    input.addEventListener("keydown", this._hideErrorMessage);
    input.addEventListener("click", this._hideErrorMessage);
  }

  /**
   * Hide the error message.
   * @param {KeyboardEvent} event - Keydown event from the input.
   * @private
   */
  _hideErrorMessage(event) {
    let error = document.getElementById(`${event.target.id}-error`);
    if (error) {
      error.style.display = "none";
    }
  }
}
