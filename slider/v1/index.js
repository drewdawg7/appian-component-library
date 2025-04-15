let componentState = {
    input: "",
    min: 0,
    max: 100,
};

Appian.Component.onNewValue(function (newValues) {
    componentState.input = newValues.input;
    componentState.min = newValues.min;
    componentState.max = newValues.max;

    const container = document.getElementById("slide-container");
    container.innerHTML = "";

    const sliderWrapper = document.createElement("div");
    sliderWrapper.className = "slider-wrapper";

    const sliderRow = document.createElement("div");
    sliderRow.className = "slider-row";

    const minLabel = document.createElement("div");
    minLabel.className = "slider-min";
    minLabel.textContent = componentState.min;

    const maxLabel = document.createElement("div");
    maxLabel.className = "slider-max";
    maxLabel.textContent = componentState.max;

    const sliderContainer = document.createElement("div");
    sliderContainer.className = "slider-track-container";

    const sliderThumbWrapper = document.createElement("div");
    sliderThumbWrapper.className = "slider-thumb-wrapper";

    const rangeSlider = document.createElement("input");
    rangeSlider.type = "range";
    rangeSlider.min = componentState.min;
    rangeSlider.max = componentState.max;
    rangeSlider.value = componentState.input;

    const valueDisplay = document.createElement("div");
    valueDisplay.className = "slider-value";
    valueDisplay.textContent = componentState.input;

    const updateVisuals = (value) => {
        const percent = ((value - componentState.min) / (componentState.max - componentState.min)) * 100;
        valueDisplay.textContent = value;
        rangeSlider.style.background = `linear-gradient(to right, #007bff ${percent}%, #ddd ${percent}%)`;

        requestAnimationFrame(() => {
            const sliderRect = rangeSlider.getBoundingClientRect();
            const offset = (percent / 100) * sliderRect.width;
            valueDisplay.style.left = `${offset}px`; // center handled by CSS
        });
    };

    rangeSlider.addEventListener("input", (e) => {
        componentState.input = e.target.value;
        updateVisuals(componentState.input);
    });

    rangeSlider.addEventListener("change", (e) => {
        componentState.input = e.target.value;
        Appian.Component.saveValue("input", componentState.input);
    });

    sliderThumbWrapper.appendChild(valueDisplay);
    sliderThumbWrapper.appendChild(rangeSlider);
    sliderContainer.appendChild(sliderThumbWrapper);

    sliderRow.appendChild(minLabel);
    sliderRow.appendChild(sliderContainer);
    sliderRow.appendChild(maxLabel);

    sliderWrapper.appendChild(sliderRow);
    container.appendChild(sliderWrapper);

    setTimeout(() => updateVisuals(componentState.input), 0);
});
