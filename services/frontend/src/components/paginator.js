import "../data/css/paginator.css";

function Paginator (props) {
    var paginationPages = []
    const countPages = parseInt(props.maxPage)
    const activePage = parseInt(props.page)
    if (countPages - activePage < 7) {
        for (let i = countPages - activePage - 1; i < countPages + 1; i++) {
            let paginationPageItemClassName = undefined
            if (i === activePage) {
                paginationPageItemClassName = "active"
            }
            if (i > 0 && i <= countPages) {
                paginationPages.push(<button id={i}
                                             key={i}
                                             className={paginationPageItemClassName}
                                             onClick={props.changePageFunction}>{i}</button>)
            }
        }
    }
    else {
        var startPage = activePage - 1
        var maxPage = activePage + 2
        if (activePage === 1) {
            startPage = startPage + 1
            maxPage = maxPage + 1
        }
        for(let i = startPage; i < maxPage; i++) {
            let paginationPageItemClassName = undefined
            if (i === activePage) {
                paginationPageItemClassName = "active"
            }
            if (i > 0 && i <= countPages) {
                paginationPages.push(<button id={i}
                                             key={i}
                                             className={paginationPageItemClassName}
                                             onClick={props.changePageFunction}>{i}</button>)
            }
        }
        paginationPages.push(<span key = "...">...</span>)
        for(let i = countPages - 2; i <= countPages; i++) {
            let paginationPageItemClassName = undefined
            if (i === activePage) {
                paginationPageItemClassName = "active"
            }
            if (i > 0 && i <= countPages) {
                paginationPages.push(<button id={i}
                                             key={i}
                                             className={paginationPageItemClassName}
                                             onClick={props.changePageFunction}>{i}</button>)
            }
        }
    }
    return <div className="pagination">
        {paginationPages}
    </div>
}

export default Paginator