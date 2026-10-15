const courseModel = require('../models/courseModel');
const enrollmentModel = require('../models/enrollmentModel');
const userModel = require('../models/userModel');
const paymentModel = require('../models/paymentModel');

async function financialReport(req, res, next) {
  try {
    const courses = await courseModel.findAll();
    const report = [];

    for (const c of courses) {
      const courseData = { course: c.title, revenue: 0, students: [] };
      const enrollments = await enrollmentModel.findByCourseId(c.id);

      for (const enr of enrollments) {
        const user = await userModel.findById(enr.user_id);
        const payment = await paymentModel.findByEnrollmentId(enr.id);

        if (payment && payment.status === 'PAID') {
          courseData.revenue += payment.amount;
        }

        courseData.students.push({
          student: user ? user.name : 'Unknown',
          paid: payment ? payment.amount : 0,
        });
      }

      report.push(courseData);
    }

    return res.json(report);
  } catch (err) {
    next(err);
  }
}

module.exports = { financialReport };
