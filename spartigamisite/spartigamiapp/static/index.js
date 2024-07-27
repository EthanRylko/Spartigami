function display_callback(text) {
    document.getElementById("infobox-content").innerHTML = text;
}

function table_callback(stats, color) {
    var cells = document.querySelectorAll(".clickable");
    cells.forEach(function(cell) {
        if (!show_grad) {
            cell.style.backgroundColor = default_color;
        } else {
            cell.style.backgroundColor = color[cell.getAttribute('cell-id')]
        }

        if (!show_stat) {
            cell.innerText = "";
        } else {
            cell.innerText = stats[cell.getAttribute('cell-id')]
        }
    });
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
            let first_day = data.first_day
            let last_day = data.last_day

            let first_home = data.first_home == "H" ? "at home vs." : "away at";
            if (data.first_win === 'N') first_win = "at a neutral site vs.";
            let last_home = data.last_home == "H" ? "at home vs." : "away at";
            if (data.last_home === 'N') last_home = "at a neutral site vs.";
            let first_win = data.first_win == "W" ? "Win" : "Loss";
            if (data.first_win === 'T') first_win = "Tie";
            let last_win = data.last_win == "W" ? "Win" : "Loss";
            if (data.last_win === 'T') last_win = "Tie";

            let first_msu_rank = data.first_msu_rank;
            let first_opp_rank = data.first_opp_rank;
            let last_msu_rank = data.last_msu_rank;
            let last_opp_rank = data.last_opp_rank;
            first_msu_rank = (first_msu_rank == 0) ? "" : `(${first_msu_rank})`;
            first_opp_rank = (first_opp_rank == 0) ? "" : `(${first_opp_rank})`;
            last_msu_rank = (last_msu_rank == 0) ? "" : `(${last_msu_rank})`;
            last_opp_rank = (last_opp_rank == 0) ? "" : `(${last_opp_rank})`;

            let first_day_str = `${first_day}. ${date_to_str(first_game)}`
            let last_day_str = `${last_day}. ${date_to_str(last_game)}`

            info_text = `<b> ${high}-${low}: </b> Score happened ${games} time`;
            info_text += (games > 1) ? "s" : "";
            info_text += ` (${record})`;
            info_text += `<br> First game: ${first_day_str}: ${first_msu_rank} ${first_win} ${first_home} ${first_opp_rank} ${first_opponent}`;
            if (games != 1) {
                info_text += `<br> Last game: ${last_day_str}: ${last_msu_rank} ${last_win} ${last_home} ${last_opp_rank} ${last_opponent}`;
            }

            callback(info_text);
        }
    })
    .catch(error => console.error('Error:', error));
    
}

function refresh_table(callback) {
    fetch(`/api/table-data/${mode}/`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            let stats = data.stats;
            let color = data.color;

            callback(stats, color);
        }
    })
    .catch(error => console.error('Error:', error));
}

function highlight(cell, on) {
    color = cell.style.backgroundColor;
    if (color == "white" || color == "silver") {
        cell.style.backgroundColor = on ? "silver" : "white";
        return;
    }

    console.log(color);
    if (color == "gray" || color == "gold") {
        cell.style.backgroundColor = on ? "gold": "gray";
    }
}

function highlight_row_col(cursor_cell, on) {
    const row = cursor_cell.parentNode;
    const cells = row.querySelectorAll("td, th");
    const col_index = Array.from(cursor_cell.parentNode.children).indexOf(cursor_cell);

    cells.forEach(cell => {
        highlight(cell, on);
    });

    const rows = row.parentNode.querySelectorAll("tr");
    const top_row = document.getElementById("header");
    highlight(top_row.querySelectorAll("th")[col_index], on);
    rows.forEach(r => {
        const cell = r.children[col_index];
        if (cell) {
            highlight(cell, on);
        }
    });

}

var mode = "count";
var show_stat = false;
var show_grad = false;
var default_color = "#008000";

document.addEventListener("DOMContentLoaded", function() {
    var cells = document.querySelectorAll(".clickable");
    const infoBox = document.getElementById("infobox");
    const infoBoxContent = document.getElementById("infobox-content");
    const infoBoxClose = document.getElementById("infobox-close");
    const showStatCheck = document.getElementById("show-stat-input");
    const showGradCheck = document.getElementById("show-grad-input");
    const dropdown = document.getElementById("mode");
    refresh_table(table_callback);

    cells.forEach(function(cell) {
        cell.style.backgroundColor = default_color;
        cell.innerText = "";
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

    showStatCheck.addEventListener("click", function(event) {
        console.log("clicked stat");
        show_stat = !show_stat;
        refresh_table(table_callback);
    });

    showGradCheck.addEventListener("click", function(event) {
        console.log("clicked grad");
        show_grad = showGradCheck.checked;
        refresh_table(table_callback);
    });

    dropdown.addEventListener("change", function() {
        mode = dropdown.value;
        refresh_table(table_callback);
    });

    const table = document.getElementById('scoretable');
    const rows = table.querySelectorAll('tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach(cell => {
            cell.addEventListener("mouseover", function () {
                highlight_row_col(cell, true);
            });
            cell.addEventListener("mouseout", function () {
                highlight_row_col(cell, false);
            });
        });
    });

});