document.addEventListener('DOMContentLoaded', () => {
const schedules = {
  employee1: [
    // array of schedule data for employee1
  ],
  employee2: [
    // array of schedule data for employee2
  ],
  employee3: [
    // array of schedule data for employee3
  ]
};
const boxes = document.querySelectorAll('.box');


boxes.forEach((box, index) => {
  box.addEventListener('click', () => {
    const employee = document.querySelector('#employeeSelect').value;
    schedules[employee][index] = true; // or store whatever schedule data you need
    console.log('Schedule data saved for employee', employee);
  });
});
const employeeSelect = document.querySelector('#employeeSelect');
employeeSelect.addEventListener('change', () => {
  const employee = employeeSelect.value;
  const scheduleData = schedules[employee];
  boxes.forEach((box, index) => {
    if (scheduleData[index]) {
      box.classList.add('scheduled');
    } else {
      box.classList.remove('scheduled');
    }
  });
});

});