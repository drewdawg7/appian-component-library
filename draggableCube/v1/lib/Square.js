export function Square({
    width = "50px",
    height = "50px",
    backgroundColor = "blue",
    top = "0px",
    left = "0px",
} = {}) {
    const square = document.createElement("div");
    square.className = "square";
    square.style.width = width;
    square.style.height = height;
    square.style.backgroundColor = backgroundColor;
    square.style.position = "absolute";
    square.style.cursor = "grab";
    square.style.top = top;
    square.style.left = left;

    return square;
}