function addTask(){
    $.ajax({
        type:"POST",
        url: "/mytasks/add_task/",
        data: JSON.stringify({ "title": document.getElementById("title").value }),
        dataType:"json",
        async: true,
        success: function(task){
            const elem = document.getElementById("no_tasks");
            if(elem){ elem.remove(); }
            addTaskToTable(task);
        }
    });
}

$.ajax({
    type:"GET",
    url: "/mytasks/get_tasks/",
    dataType:"json",
    async: true,
    success: function(tasks){
        if (typeof tasks !== 'undefined' && tasks.length > 0){
            for(const task of tasks){
                addTaskToTable(task);
            }
        }
        else{
            const p = document.createElement("p");
            p.id = "no_tasks";
            p.innerText = "No tasks yet";
            document.getElementById("my-tasks").appendChild(p);
        }
    }
});


function addTaskToTable(task){
    const tr = document.createElement("tr");
    const td1 = document.createElement("td");
    const td2 = document.createElement("td");
    const toggle = document.createElement("input");
    const title = document.createElement("span");

    tr.id = task["id"];
    td1.style = "width: 5%";

    toggle.type = "checkbox";
    toggle.id = "checkbox"+task["id"];
    toggle.name = "task_checkbox"
    toggle.addEventListener("input", function() {
        const taskId = task["id"];
        removeTask(taskId);
    });

    title.innerText = task["title"];
    td2.style = "text-align: left";

    document.getElementById("my-tasks").appendChild(tr);
    tr.appendChild(td1);
    td1.appendChild(toggle);
    tr.appendChild(td2);
    td2.appendChild(title);
}


function removeTask(taskId){
    const checkbox = document.getElementById("checkbox"+taskId);
    if(checkbox){
        if(checkbox.checked){
            $.ajax({
                type:"POST",
                url: "/mytasks/remove_task/",
                data: JSON.stringify({ "id": taskId }),
                dataType:"json",
                async: true,
                success: function(task){
                    removeTaskFromTable();
                }
            });
        }
    }
}


function removeTaskFromTable(){
    var checkedBoxes = document.querySelectorAll('input[name=task_checkbox]:checked');
    checkedBoxes[0].parentNode.parentNode.remove();
}