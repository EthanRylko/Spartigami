function display_callback(text) {
    document.getElementById("infobox_content").innerHTML = text;
}

function date_to_str(date) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let split_result = date.split("-");
    if (split_result[2][0] === '0') {
        split_result[2] = split_result[2].substring(1);
    }

    return `${months[split_result[1] - 1]}. ${split_result[2]}, ${split_result[0]}`;
}

function grab_score_pair(cell_id, callback) {
    let info_text;
    fetch(`/api/cell-data/${cell_id}/`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            let games = data.games;
            let high = data.high;
            let low = data.low;
            let first_game = data.first_game;
            let last_game = data.last_game;
            let record = data.record;
            let first_opponent = data.first_opponent;
            let last_opponent = data.last_opponent;
            let first_home = data.first_home == "H" ? "at home vs." : "away at";
            if (data.first_win === 'N') first_win = "at a neutral site vs.";
            let last_home = data.last_home == "H" ? "at home vs." : "away at";
            if (data.last_home === 'N') last_home = "at a neutral site vs.";
            let first_win = data.first_win == "W" ? "Win" : "Loss";
            if (data.first_win === 'T') first_win = "Tie";
            let last_win = data.last_win == "W" ? "Win" : "Loss";
            if (data.last_win === 'T') last_win = "Tie";
            let first_day = data.first_day
            let last_day = data.last_day

            let first_day_str = `${first_day}. ${date_to_str(first_game)}`
            let last_day_str = `${last_day}. ${date_to_str(last_game)}`

            info_text = `<p> <b> ${high}-${low}: </b> Score happened ${games} time`;
            info_text += (games > 1) ? "s" : "";
            info_text += ` (${record}) </p>`;
            info_text += `<p> First game: ${first_day_str}: ${first_win} ${first_home} ${first_opponent} </p>`;
            if (games != 1) {
                info_text += `<p> Last game: ${last_day_str}: ${last_win} ${last_home} ${last_opponent} </p>`;
            }

            callback(info_text);
        }
    })
    .catch(error => console.error('Error:', error));
    
}

document.addEventListener("DOMContentLoaded", function() {
    var cells = document.querySelectorAll(".clickable");
    var infoBox = document.getElementById("infobox");
    var infoBoxContent = document.getElementById("infobox_content");
    var infoBoxClose = document.getElementById("infobox_close");

    cells.forEach(function(cell) {
        cell.addEventListener("click", function() {
            infoBox.style.display = 'block';
            infoBoxContent.innerHTML = "<br> <br> ...";
            let rect = cell.getBoundingClientRect();
            infoBox.style.top = (window.scrollY + rect.top + cell.offsetHeight) + "px";
            infoBox.style.left = (window.scrollX + rect.left) + "px";

            let cell_id = cell.getAttribute("cell-id");
            grab_score_pair(cell_id, display_callback);
        });
    });

    infoBoxClose.addEventListener("click", function() {
        infoBox.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target == infoBox) {
            infoBox.style.display = "none";
        }
    });
});