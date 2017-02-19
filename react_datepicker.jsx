var React = require('react');
var DayPicker = require('react-day-picker');
var { DateUtils } = require('react-day-picker');
var LocaleUtils = require('react-day-picker/moment');

var Reflux = require('reflux');


var UserInfoAction = require('actions/UserInfoAction');
var UserInfoStore = require('stores/UserInfoStore');

var moment = require('moment');

var currentYear = (new Date()).getFullYear();
var fromMonth = new Date(currentYear-50, 0, 1, 0, 0);
var toMonth = new Date(currentYear, 11, 31, 23, 59);

// Component will receive date, locale and localeUtils props
function YearMonthForm({ date, localeUtils, onChange }) {
  var months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];

	var rows = [];

  for (var i = fromMonth.getFullYear(); i <= toMonth.getFullYear(); i++) {
  	if ( i == 1996) {
  		rows.push(<option key={i} value={i} selected>{i}</option>);
  	}else{
    	rows.push(<option key={i} value={i}>{i}</option>);
  	}
  }

  var handleChange= function(e){
    var { year, month } = e.target.form;
    onChange(new Date(year.value, month.value));
  };

  return (
    <form className="DayPicker-Caption">
      <select name="month" key={date.getMonth()} onChange={handleChange} value={date.getMonth()}>
        {months.map((month, i) =>
          <option key={i} value={i}>
            {month}
          </option>)
        }
      </select>
      <select name="year" key="year" onChange={handleChange}>
      	{rows}
      </select>
     
    </form>
  );
}

var DatePicker = React.createClass({

	getInitialState: function(){
        //	모든 마운트 메소드에서 단 한번만 호출되며, 컴포넌트에 상태를 부여
        var initialMonth = new Date('1996-01-01');
        return { 
            selectedDay: null,
        	value : moment().format('L'),
        	initialMonth,
        };
    },
    mixins: [
    	Reflux.connect(UserInfoStore, 'userData')
    ],
	render: function(){

		var inputStyle = {
			fontSize:15,
			height:19,
			display:'inline-block',
			color:"#6b6b6b",
			float:"right",
			textAlign:"right"
		}

		var datePickerStyle = {
			float: "right",
			marginLeft:-5,
			width:"auto",
			right:0,
			height:"auto",
			padding:"4px 4px 4px 4px",
			backgroundColor:"white",
			position:"absolute",
			zIndex:10,
		}

		var row = null;
		row = (
			<div>
				<p id="formattedSelectedDate" type="hidden"/>
				<div>
					<p id="inputView" onClick={this.inputBtnClick} style={inputStyle}>{this.state.selectedDay ? this.state.selectedDay.toLocaleDateString() : "연도.원.일"}</p>
        		</div>
        		<br/>
        		<div style={datePickerStyle} id="dateContainer">
        			<DayPicker
        				localeUtils={LocaleUtils}
        				locale="ko"
        			    initialMonth={this.state.initialMonth}
        				id="datePicker"
        				fromMonth={fromMonth}
          				toMonth={toMonth}
          				captionElement={
            				<YearMonthForm onChange={initialMonth => this.setState({ initialMonth })} />
          				}
          				selectedDays={day => DateUtils.isSameDay(this.state.selectedDay, day)}
          				onDayClick={this.onDayClick}/>
        		</div>
      		</div>
      	)

		return row;
	},

	onDayClick: function(e, day, {selected}){

		console.log("selected day = "+moment(day).format("L"));
	
		this.setState({
			value : moment(day).format('L'),
			selectedDay: selected ? null : day,
		});
	
		UserInfoAction.addBirthDate(moment(day).format("YYYY-MM-DD"));
		var datePicker = document.getElementById("dateContainer");
		datePicker.style.display= "none";		

	},

	inputBtnClick :function(){

		var inputView = document.getElementById("inputView");
		var datePicker = document.getElementById("dateContainer");
		var confirmBtn = document.getElementById("confirmBtn");

		inputView.style.display = "inline-block";
		datePicker.style.display= "inline-block";
		confirmBtn.style.display = "inline-block";
	},
});

module.exports = DatePicker;

