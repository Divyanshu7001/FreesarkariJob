const flash_box = document.getElementById("flash_message");
flash_msg = document.getElementsByClassName("flash_msg");
Array.from(flash_msg).forEach((element) => {
  //   setTimeout(() => {
  //     element.classList.add("hide");
  //   }, 5000);

  element.addEventListener("click", () => {
    element.classList.toggle("hide");
    console.info("do");
  });
});
