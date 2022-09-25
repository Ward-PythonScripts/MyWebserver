
//globals
let given_color_id = 0;
let drawn_chart = null;

function draw_laps_from_session(data,session_index){
    set_session_info_tag(data,session_index);
    label_array = get_labels(data,session_index);
    datasets_array = get_laptimes_as_data(data,session_index);
    const ctx = document.getElementById('myChart').getContext('2d');
    drawn_chart = new Chart(ctx,{
        type:'line',
        data: {
            labels: label_array,
            datasets: datasets_array
        },
        options: {
            scales: {
                y: {
                title:{
                    display:true,
                    text:'Laptime (s)',
                    font:{
                        size:30
                    }
                },
                ticks:{
                    callback: function(value,index,ticks){
                        return value.toFixed(3);
                    },
                },
                grid:{
                    display:true,
                    drawBorder:false,
                    drawOnChartArea:true,
                    drawTicks:false,
                    color:'rgba(255, 255, 255, 0.2)',
                    borderDash:[8,4],
                }
                },
                x:{
                title:{
                    display:true,
                    text:'Lap',
                    font:{
                        size:30
                    }
                }
                }
            },
            plugins:{
                zoom:{
                    pan:{
                        enabled:true,
                        mode:'y',
                        overScaleMode:'x',
    
                    },
                    zoom:{
                        wheel:{
                            enabled:true
                        },
                        drag:{
                            enabled:true,
                            modifierKey:'shift'
                        },
                        mode: 'y'
                    }
                }
            }

            }
    })
}
function get_new_color(){
    const colors = [
        'rgba(253, 0, 0, 0.8)',
        'rgba(253, 198, 0, 0.8)',
        'rgba(203, 253, 0, 0.8)',
        'rgba(0, 253, 66, 0.8)',
        'rgba(0, 253, 192, 0.8)',
        'rgba(0, 198, 253, 0.8)',
        'rgba(0, 129, 253, 0.8)',
        'rgba(0, 40, 253, 0.8)',
        'rgba(108, 0, 253, 0.8)',
        'rgba(213, 0, 253, 0.8)',
        'rgba(253, 0, 203, 0.8)',
        'rgba(253, 0, 155, 0.8)',
        'rgba(253, 0, 92, 0.8)',
        'rgba(253, 0, 0, 0.8)',
        'rgba(29, 253, 0, 0.8)',
        'rgba(224, 253, 0, 0.8)',
        'rgba(253, 171, 0, 0.8)'
    ];
    if (given_color_id >= colors.length){
        given_color_id = colors.length-1;
    }
    color = colors[given_color_id];
    given_color_id ++;
    return color;
}
function get_latest_session_index(data){
    var latest_session_id = 0;
    var latest_session_time = 0;
    var latest_sessoin_index = 0;
    for(var key in Object.keys(data)){
        if (data[key].session.timestamp > latest_session_time){
            latest_session_time = data[key].session.timestamp;
            latest_session_id = data[key].session.session_id;
            latest_sessoin_index = key;
        }
    }
    return latest_sessoin_index;
}
function get_labels(data,session_index){
    var max_number_of_laps = 0;
    for(var key in Object.keys(data[session_index].session.drivers_laps)){
        driven_laps = data[session_index].session.drivers_laps[key].laptimes.length;
        if(max_number_of_laps<driven_laps){
            max_number_of_laps = driven_laps;
        }
    }
    max_number_of_laps_as_labels = [];
    integ = 1;
    while(integ <= max_number_of_laps){
        max_number_of_laps_as_labels.push(integ);
        integ ++;
    }
    return max_number_of_laps_as_labels;

}
function get_laptimes_as_data(data,session_index){
    datasets_array = [];
    for(var key2 in Object.keys(data[session_index].session.drivers_laps)){
        newcolor = get_new_color();
        datasets_array.push({
            label: String(data[session_index].session.drivers_laps[key2].driver_name) + " ["+String(data[session_index].session.drivers_laps[key2].kart_nr)+"]",
            data: laptimes_to_seconds_laptimes(data[session_index].session.drivers_laps[key2].laptimes),
            borderColor: newcolor,
            backgroundColor: newcolor,
        })
    }
    return datasets_array;
}
function laptimes_to_seconds_laptimes(laptimes){
    newlist = [];
    for ( var key in Object.keys(laptimes)){
        newlist.push(millis_to_seconds(laptimes[key]));
    }
    return newlist;
}
function millis_to_seconds(millis){
    return millis/1000;
}

function set_session_info_tag(data,session_index){
    session = data[session_index].session;
    session_tag = document.getElementById("session_info");
    date_string = timestamp_to_string(session.timestamp);
    session_tag.innerHTML = date_string;
}

function timestamp_to_string(timestamp){
    var date = new Date(timestamp*1000); //timestamps are saved in seconds
    var date_string = String(date.getDate()) + "/" + String(date.getMonth()) + "/" 
        + String(date.getFullYear()) + " " + String(date.getHours()) + ":";
    //following need if the minutes are 0 -> better formatting
    if(date.getMinutes() == 0){
        date_string += "00"
    }
    else{
        date_string += String(date.getMinutes());
    }
    return String(date_string);
}


function inflate_session_buttons(data){
    const buttons_div = document.getElementById("session_buttons");
    var sorted_data = data;
    sorted_data.sort(function(a,b){
        return a.session.timestamp - b.session.timestamp;
    });
    for(var session_key in Object.keys(sorted_data)){
        button = generate_session_button(sorted_data[session_key].session,session_key);
        buttons_div.appendChild(button);
    }
}

function generate_session_button(session,index){
    date_string = timestamp_to_string(session.timestamp);
    button = document.createElement("button");
    button.setAttribute("id",index);
    button.setAttribute("onclick","session_selector_button_callback(this.id)");
    button.innerHTML = date_string;
    return button;
}

function session_selector_button_callback(session_index){
    //if last character was an / -> can just add if not than it was a number which we need to remove first
    old_url = window.location.href;
    if (old_url.charAt(old_url.length - 1) != "/")
        old_url = old_url.slice(0,-1);
    window.location.href = old_url + String(session_index);

    
}

function hide_all_button_callback(){
    try{
        var index = 0;
        while (true ){
            //untill fails set dataset to hidden
            drawn_chart.hide(index);
            index ++;
        }
    }
    catch{
        //ignore, just means that all have been hidden
    }
}

function show_all_button_callback(){
    try{
        var index = 0;
        while (true ){
            //untill fails set dataset to hidden
            drawn_chart.show(index);
            index ++;
        }
    }
    catch{
        //ignore, just means that all have been hidden
    }
}


