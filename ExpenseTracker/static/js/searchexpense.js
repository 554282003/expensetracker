const searchfield = document.querySelector("#searchfield");
const tableoutput = document.querySelector(".table-output")
const apptable = document.querySelector(".app-table")
const pagination = document.querySelector(".pagination-container")
const tabledata  = document.querySelector(".table-data")
const noresult = document.querySelector(".no-results")

tableoutput.style.display = "none";

searchfield.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  if (searchValue.trim().length > 0) {
    pagination.style.display = "none";
    tabledata.innerHTML = ""; // Clear previous table data
    fetch("/search-expense", {
      body: JSON.stringify({ searchfield: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        apptable.style.display = "none";
        tableoutput.style.display = "block";

        if (data.length === 0) {
          noresult.style.display="block"
          tableoutput.style.display = "none";
        } else {
          noresult.style.display="none"
          data.forEach((item) => {
            tabledata.innerHTML += `
            <tr>
            <td>${item.amount}</td>
            <td>${item.category}</td>
            <td>${item.description}</td>
            </tr>
            `;
          });
        }
      })
    }else{
    noresult.style.display="none"
    apptable.style.display = "block";
    pagination.style.display = "block";
    tableoutput.style.display = "none";
  }
});
