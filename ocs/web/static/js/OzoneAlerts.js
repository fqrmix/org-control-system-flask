class Ozone {
  static fire(
    icon,
    message,
    position,
    type = "notification",
    options = {},
    onConfirm = function () {},
    onCancel = function () {}
  ) {
    // Creates essential elements
    const el = document.createElement("div");
    el.className = "Ozone";
    const divIcon = document.createElement("div");
    divIcon.className = "OzoneIcon";
    const divMessage = document.createElement("div");
    divMessage.className = "OzoneMessage";

    // Appends elements to parent element
    el.appendChild(divIcon);
    el.appendChild(divMessage);

    // Sets message based on parameter "message"
    divMessage.innerHTML = "<p>" + message + "</p>";

    // Handles icon selection based on parameter "icon"
    if (icon == "success") {
      divIcon.innerHTML = '<i class="fas fa-check"></i>';
    } else if (icon == "error") {
      divIcon.innerHTML = '<i class="fas fa-times"></i>';
    } else if (icon == "info") {
      divIcon.innerHTML = '<i class="fas fa-info"></i>';
    }
    // Creates Ozone instance of type "dialog" based on "type" parameter
    if (type == "dialog") {
      // Necessary changes to styling for dialog
      el.style.flexDirection = "column";
      divIcon.style.position = "relative"; 
      divIcon.style.left = "0px";
      divIcon.style.marginTop = "15px";

      // Creates necessary table elements for dialog
      const divControls = document.createElement("div");
      divControls.className = "OzoneControls";

      const btnConfirm = document.createElement("button");
      btnConfirm.className = "OzoneBtnConfirm";
      btnConfirm.innerHTML = "Confirm";
      const btnCancel = document.createElement("button");
      btnCancel.className = "OzoneBtnCancel";
      btnCancel.innerHTML = "Cancel";

      // Appends elements to parent element
      el.appendChild(divControls);
      divControls.appendChild(btnConfirm);
      divControls.appendChild(btnCancel);

      // Handles functions on dialog button click
      btnConfirm.onclick = function () {
        onConfirm();
        removeOzoneAlert(el);
      };

      btnCancel.onclick = function () {
        onCancel();
        removeOzoneAlert(el);
      };

      // Sets dialog specific options based on "options" object parameter
      if (Object.keys(options).length > 0) {
        if (options.confirmButtonText) {
          btnConfirm.innerHTML = options.confirmButtonText;
        }
        if (options.cancelButtonText) {
          btnCancel.innerHTML = options.cancelButtonText;
        }
        if (options.confirmButtonColor) {
          btnConfirm.style.backgroundColor = options.confirmButtonColor;
        }
        if (options.cancelButtonColor) {
          btnCancel.style.backgroundColor = options.cancelButtonColor;
        }
        if (options.confirmButtonRadius) {
          btnConfirm.style.borderRadius = options.confirmButtonRadius;
        }
        if (options.cancelButtonRadius) {
          btnCancel.style.borderRadius = options.cancelButtonRadius;
        }
      }
    }

    // Handles position based on parameter "position"
    switch (position) {
      case "top-left":
        el.style.left = 0;
        el.style.top = 0;
        break;

      case "top-right":
        el.style.right = 0;
        el.style.top = 0;
        break;

      case "top-middle":
        el.style.left = 0;
        el.style.right = 0;
        el.style.marginLeft = "auto";
        el.style.marginRight = "auto";
        break;

      case "bottom-left":
        el.style.left = 0;
        el.style.bottom = 0;
        break;

      case "bottom-middle":
        el.style.left = 0;
        el.style.right = 0;
        el.style.bottom = 0;
        el.style.marginLeft = "auto";
        el.style.marginRight = "auto";
        break;

      case "bottom-right":
        el.style.right = 0;
        el.style.bottom = 0;
        break;

      case "center":
        el.style.left = 0;
        el.style.right = 0;
        el.style.marginLeft = "auto";
        el.style.marginRight = "auto";
        el.style.marginTop = "20%";
        break;
    }

    // Sets general options based on "options" object passed as parameter
    if (Object.keys(options).length > 0) {
      if (options.backgroundColor) {
        el.style.backgroundColor = options.backgroundColor;
      }
      if (options.fontColor) {
        divMessage.style.color = options.fontColor;
      }
      if (options.iconColor) {
        divIcon.style.color = options.iconColor;
      }
      if (options.borderRadius) {
        el.style.borderRadius = options.borderRadius;
      }
      if (options.border) {
        el.style.border = options.border;
      }
    }

    // Finally appends Ozone alert element to document body
    document.body.appendChild(el);

    // Handles animations upon creation and deletion of Ozone element
    setTimeout(() => {
      el.style.animation = "ozPulse 2s infinite";
    }, 1000);

    // Handles behavior of Ozone alert upon deletion based on type
    if (type == "notification") {
      setTimeout(() => {
        el.style.animation = "ozFadeOut ease 1s";
      }, 7000);

      setTimeout(() => {
        el.parentNode.removeChild(el);
      }, 8000);
    }

    // Function that removes a given Ozone-element with a fadeOut-effect
    function removeOzoneAlert(element) {
      element.style.animation = "ozFadeOut ease 0.5s";
      setTimeout(() => {
        element.parentNode.removeChild(element);
      }, 495);
    }
  }
}
