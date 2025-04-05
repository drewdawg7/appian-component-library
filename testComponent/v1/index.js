let componentState = {
    input: "",
};

Appian.Component.onNewValue(function (newValues) {
    console.log("[onNewValue] Received from Appian:", newValues);

    componentState.input = newValues.input;

    const container = document.getElementById("test-container");
    container.innerHTML = "";

    const textField = document.createElement("input");
    textField.type = "text";
    textField.value = componentState.input;

    textField.addEventListener("input", function (e) {
        componentState.input = e.target.value;
        Appian.Component.saveValue("input", componentState.input);
    });

    container.appendChild(textField);
});
