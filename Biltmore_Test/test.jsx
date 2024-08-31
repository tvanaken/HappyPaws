import React, { useState } from "react";
import { createRoot } from "react-dom/client";

const SubscribeButton = (props) => {
    // Write your code here
    const [subscribe, setSubscribe] = useState(false);

    const handleClick = () => {
        setSubscribe(true);
    };

    return subscribed ? (
        <p>Thank you for subscribing!</p>
    ) : (
        <button onClick={handleClick}>Click to subscribe!</button>
    );
};

document.body.innerHTML = "<div id='root'> </div>";
const root = createRoot(document.getElementById("root"));
root.render(<SubscribeButton />);

setTimeout(() => console.log(document.body.innerHTML), 100);
