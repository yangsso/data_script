var React = require('react');
var moment = require('moment');
var $ = require('jquery');
var UserInfoStore = require('stores/UserInfoStore');
var UserInfoAction = require('actions/UserInfoAction');
var Reflux = require('reflux');


var DateInputText = React.createClass({
  
  	getInitialState: function(){
        //  모든 마운트 메소드에서 단 한번만 호출되며, 컴포넌트에 상태를 부여
        return {
            year:null,
            month:null,
            day:null,
        };
    },
    mixins: [
        Reflux.connect(UserInfoStore, 'userData')
    ],
	render: function(){

		var containerStyle = {
			width:"100%",
			display:"inline-block",
			float:"right",
		}

		var yearStyle = {
			width:"40px",
			fontSize:"15px",
			border:"none",
			color:"#6b6b6b",
			textAlign:"right"
		}

		var monthDayStyle = {
			width:"20px",
			fontSize:"15px",
			border:"none",
			color:"#6b6b6b",
			textAlign:"right"			
		}

		var dashStyle = {
			textAlign:"right",
			color:"#d0d0d0",
			margin:"0px 0px 0px 3px",
		}


		var row = (
			<div style={containerStyle}>
				<input onChange={this.textChange} style={yearStyle} id="_year" type="number" placeholder="0000"/>
				<span className="dash_line1" style={dashStyle} >-</span>
				<input onChange={this.textChange} style={monthDayStyle} id="_month" type="number" placeholder="00"/>
				<span className="dash_line2" style={dashStyle} >-</span>
				<input onChange={this.textChange} style={monthDayStyle} id="_day" type="number" placeholder="00"/>
			</div>)

		return row;

	},

	checkValidDate: function(){
		var year = document.getElementById("_year");
		var month = document.getElementById("_month");
		var day = document.getElementById("_day");

		var date = year.value+"-"+month.value+"-"+day.value;
		var isValidDate = moment(date, "YYYY-MM-DD", true).isValid();

		if (!isValidDate) {
			alert("올바른 날짜를 입력해주세요 :)");
			day.value = null;
		}else{
			UserInfoAction.addBirthDate(date);
		}
	},
	textChange: function(e){
		var year = document.getElementById("_year").value;
		var month = document.getElementById("_month").value;
		var day = document.getElementById("_day").value;

		var id = e.target.id;
		var value = e.target.value;

		var valueLen = value.trim().length;

		if (id == "_year") {
			if (valueLen >= 4) {
				e.target.value = value.substring(0,4);
			}
			if (valueLen == 4) {

				if (value > 2016 || value < 1950) {
					alert("올바른 년도를 입력해주세요 :)");
					e.target.value = null;
					return;
				}else{
					$(".dash_line1").css("color","#6b6b6b");		
				}
				document.getElementById("_month").focus();
			}
		}else if(id == "_month"){
			if (valueLen >= 2) {
				e.target.value = value.substring(0,2);
				if (value > 12 || value < 1) {
					alert("올바른 달을 입력해주세요 :)");
					e.target.value = null;
					return;
				}else{
					$(".dash_line2").css("color","#6b6b6b");	
				}	
				document.getElementById("_day").focus();
			}
		}else if(id == "_day"){
			if(valueLen == 2){
				if (value > 31 || value < 1) {
					alert("올바른 날을 입력해주세요 :)");
					e.target.value = null;
					return;
				}
			}
		}

		if (year != null && month != null && day != null && year != undefined && month != undefined && day != undefined) {
			if (year.trim().length == 4 && month.trim().length == 2 && day.trim().length == 2) {
				this.checkValidDate();
			}
		}

	},

});

module.exports = DateInputText;

