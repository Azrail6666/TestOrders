import * as React from "react";
import axios from "axios";

import TopBar from "./components/topBar";
import TotalCounter from "./components/totalCounter";
import Table from "./components/table";
import OrdersChart from "./components/chart";
import Paginator from "./components/paginator";


import charIcon from "./data/img/chartIcon.svg"
import tableIcon from "./data/img/tableIcon.svg"


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isTableShow: true,
      page: 1,
      maxPage: 0,
      totalCount: 0,
      ordersHead: [],
      orders: [],
      ordersStats: {
        labels: [],
        data: []
      }
    }
    this.showTableOrChart = this.showTableOrChart.bind(this)
    this.updateOrders = this.updateOrders.bind(this)
    this.updateOrdersStats = this.updateOrdersStats.bind(this)
    this.changePage = this.changePage.bind(this)
  }

  componentDidMount() {
    this.updateOrders()
    this.updateOrdersStats()
    this.updatorOrdersInterval = setInterval(
      () => this.updateOrders(),
      10000
    );
    this.updatorOrdersStatsInterval = setInterval(
      () => this.updateOrdersStats(),
      10000
    );
  }

  componentWillUnmount() {
    clearInterval(this.updatorOrdersInterval);
    clearInterval(this.updatorOrdersStatsInterval);
  }

  showTableOrChart() {
    this.setState({
      isTableShow: !this.state.isTableShow
    })
  }

  updateOrders() {
    var body = new FormData()
    body.append("page", this.state.page)
    axios({
      method: "POST",
      url: "http://127.0.0.1:9000/get_orders",
      data: body
    }).then((response) => {
      if(response.data.status) {
        this.setState({
          ordersHead: response.data.data.ordersHead,
          orders: response.data.data.orders,
          totalCount: response.data.data.total_count,
          maxPage: Math.ceil(response.data.data.total_count / 20)
        })
      }
      else {
        console.log(response.data.error)
      }
    })
  }

  updateOrdersStats() {
    axios({
      method: "GET",
      url: "http://127.0.0.1:9000/get_days_statistic"
    }).then((response) => {
      if(response.data.status) {
        this.setState({ordersStats: response.data.data})
      }
      else {
        console.log(response.data.error)
      }
    })
  }

  async changePage(event) {
    const new_page = parseInt(event.target.id)
    if (new_page > 0 && new_page <= this.state.maxPage) {
      await this.setState({page: new_page})
    }
    this.updateOrders()
  }

  render () {
    var tableChartButtonIcon = charIcon
    var tableChart = <Table tableHead = {this.state.ordersHead} tableBody = {this.state.orders}/>
    var pagination = <Paginator page = {this.state.page}
                                maxPage = {this.state.maxPage}
                                changePageFunction = {this.changePage}/>
    if (!this.state.isTableShow) {
      tableChartButtonIcon = tableIcon
      tableChart = <OrdersChart labels = {this.state.ordersStats.labels}  data = {this.state.ordersStats.data}/>
      pagination = null
    }
    return (
      <div id = "app">
        <TopBar />
        <div className = "main-data">
          <div className = "table-chart">
              <div className = "table-chart-header">
                <button className = "table-chart-button" onClick = {this.showTableOrChart}>
                  <img src = {tableChartButtonIcon} alt = "Кнопка переключения"/>
                </button>
              </div>
            <div className = "table-chart-data">
              {tableChart}
              {pagination}
            </div>
          </div>
          <TotalCounter totalCount = {this.state.totalCount}/>
        </div>
      </div>
    );
  }
}

export default App;
