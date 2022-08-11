import LogoImage from "../data/img/logo.png";
import "../data/css/topBar.css";


function TopBar (){
    return (<div className = "top-bar">
        <div className = "top-bar-logo">
            <img src = {LogoImage} alt = "Логотип"/>
        </div>
    </div>)
}


export default TopBar