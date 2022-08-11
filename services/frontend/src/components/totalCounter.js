import * as React from "react";

import "../data/css/totalCounter.css";

/*
    Element for displaying the total number of orders
 */
function TotalCounter (props) {
    return <div className = "total-counter">
        <div className = "total-counter-title">
            <span>Total</span>
        </div>
        <div className = "total-counter-value">
            <span>{props.totalCount}</span>
        </div>
    </div>
}

export default TotalCounter