function createElement(tag, attrs) {
  const keys = Object.keys(attrs || {});
  const el = document.createElement(tag);
  for (let i = 0; i < keys.length; ++i) {
    el.setAttribute(keys[i], attrs[[keys[i]]]);
  }
  return el;
}
function add_bookmark_button() {
  var bookmarkButton = createElement("button", { class: "bookmark-button" });
  bookmarkButton.innerHTML =
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"/></svg>';

  document.querySelector(".name").append(bookmarkButton);

  bookmarkButton.addEventListener("click", () => {
    if (bookmarkButton.classList.contains("yellow-bookmark-button")) {
      bookmarkButton.classList.remove("yellow-bookmark-button");
      chrome.runtime.sendMessage(
        {
          message: "delete_bookmark",
          payload: window.location.pathname.substring(2),
        },
        (response) => {
          if (response.message === "success") {
            console.log("success delete bookmark");
          }
        }
      );
    } else {
      bookmarkButton.classList.add("yellow-bookmark-button");
      chrome.runtime.sendMessage(
        {
          message: "add_bookmark",
          payload: window.location.pathname.substring(2),
        },
        (response) => {
          if (response.message === "success") {
            console.log("success add bookmark");
          }
        }
      );
    }
  });

  chrome.runtime.sendMessage(
    {
      message: "is_bookmarked",
      payload: window.location.pathname.substring(2),
    },
    (response) => {
      console.log(response.is_bookmarked);
      if (response.is_bookmarked) {
        bookmarkButton.classList.add("yellow-bookmark-button");
      } else {
        bookmarkButton.classList.remove("yellow-bookmark-button");
      }
    }
  );
}

console.log(document.querySelector(".bookmark-button"));
if (document.querySelector(".bookmark-button") == null) {
  add_bookmark_button();
  console.log("SUCCES add bookmark button");
}
