import { createAnimatable } from 'animejs';

let componentState = {
    percentage: 0,
    barColor: "",
    borderColor: ""
};

Appian.Component.onNewValue(function (newValues) {
    console.log("[onNewValue] Received from Appian:", newValues);

    componentState.percentage = newValues.percentage || 0;
    componentState.barColor = newValues.barColor || "green";
    componentState.borderColor = newValues.borderColor;

    const container = document.getElementById("bar-container");
    container.innerHTML = "";
    container.style.display = "inline-block";
    container.style.width = "300px";
    container.style.height = "15px";
    container.style.borderRadius = "20px";
    container.style.backgroundColor = "#f3f3f3";
    container.style.overflow = "hidden";

    if (componentState.borderColor && componentState.borderColor !== "") {
        container.style.border = `1px solid ${componentState.borderColor}`;
    } else {
        container.style.border = "none";
    }

    const fill = document.createElement("div");
    fill.style.height = "100%";
    fill.style.width = componentState.percentage + "%";
    fill.style.backgroundColor = componentState.barColor;
    fill.style.borderRadius = "20px 0 0 20px";
    fill.style.position = "relative";
    fill.style.overflow = "hidden";

    const shimmer = document.createElement("div");
    shimmer.style.position = "absolute";
    shimmer.style.top = "0";
    shimmer.style.left = "0";
    shimmer.style.height = "100%";
    shimmer.style.width = "75%";
    shimmer.style.background = "linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.6) 50%, rgba(255,255,255,0) 100%)";
    shimmer.style.pointerEvents = "none";

    fill.appendChild(shimmer);
    container.appendChild(fill);

    const shimmerAnim = createAnimatable(shimmer, {
        translateX: 100,
        ease: 'linear',
        duration: 1000
    });

    function shimmerLoop() {
        shimmerAnim.translateX(-100, 0);
        shimmerAnim.translateX(200, 2000, 'linear');
        setTimeout(shimmerLoop, 2000);
    }

    shimmerLoop();
});
