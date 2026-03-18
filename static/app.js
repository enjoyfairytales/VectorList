const todoItems = document.querySelectorAll(".todo-item");
const confirmForms = document.querySelectorAll("form[data-confirm]");

todoItems.forEach((item) => {
  const openButton = item.querySelector('[data-action="edit-open"]');
  const cancelButton = item.querySelector('[data-action="edit-cancel"]');
  const input = item.querySelector(".todo-edit input");

  if (openButton) {
    openButton.addEventListener("click", () => {
      item.classList.add("is-editing");
      if (input) {
        input.focus();
        input.select();
      }
    });
  }

  if (cancelButton) {
    cancelButton.addEventListener("click", () => {
      item.classList.remove("is-editing");
    });
  }
});

confirmForms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    const message = form.getAttribute("data-confirm") || "Are you sure?";
    if (!window.confirm(message)) {
      event.preventDefault();
    }
  });
});
