$(document).ready(function () {
  $(".datatable").DataTable({
    language: {
      url: "{% static 'js/langue/fr_fr.json' %}",
    },
    pageLength: 15,
    lengthMenu: [5, 10, 25, 50, 100],
    order: [[0, "asc"]],
    searching: true,
    paging: true,
    info: true,
    responsive: true,
  });
});
