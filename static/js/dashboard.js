
      function showTab(tabName) {
          var i;
          var x = document.getElementsByClassName("tab-content");
          for (i = 0; i < x.length; i++) {
              x[i].style.display = "none";
          }
          var tabs = document.getElementsByClassName("tab");
          for (i = 0; i < tabs.length; i++) {
              tabs[i].classList.remove("active");
          }
          document.getElementById(tabName).style.display = "block";
          document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add("active");
      }
  
      // Initially show the "completed" tab
      document.getElementById('completed').style.display = 'block';
