import { createDraggable } from 'animejs';
import { Square } from './lib/Square.js';

let componentState = {
    input: "",
};


Appian.Component.onNewValue(function (newValues) {
    console.log("[onNewValue] Received from Appian:", newValues);

    componentState.input = newValues.input;

    const container = document.getElementById("cube-container");
    container.innerHTML = "";
    container.style.height = "400px";
    container.style.width = "400px";
    container.style.position = "relative";
    container.style.overflow = "hidden";
    container.style.border = "1px solid black";

    const square = Square({});

    console.log('Container:', container);

    container.appendChild(square);

    createDraggable(".square", {
        container: container,
        containerFriction: 1,
    });

});

