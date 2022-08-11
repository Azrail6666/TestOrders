import * as React from "react";
import "../data/css/table.css"

/*
    Element for displaying the table of orders
 */
function Table (props) {
    const tableHeadItems = props.tableHead.map((tableHeadItemData) => {
        return <th key = {tableHeadItemData}>{tableHeadItemData}</th>
    })
    const tableBodyItems = props.tableBody.map((tableBodyItemData => {
        const tableBodyItemColumns = tableBodyItemData.map((tableBodyItemColumnData) => {
            return <td key = {tableBodyItemColumnData}>{tableBodyItemColumnData}</td>
        })
        return <tr key = {tableBodyItemData[0]}>{tableBodyItemColumns}</tr>
    }))
    return <table className = "data-table">
        <thead>
            <tr>
                {tableHeadItems}
            </tr>
        </thead>
        <tbody>
            {tableBodyItems}
        </tbody>
    </table>
}

export default Table