const db = require('./database');

async function create(userId, courseId) {
  const result = await db.run(
    'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)',
    [userId, courseId]
  );
  return result.lastID;
}

async function findByCourseId(courseId) {
  return db.all('SELECT * FROM enrollments WHERE course_id = ?', [courseId]);
}

async function deleteByUserId(userId) {
  return db.run('DELETE FROM enrollments WHERE user_id = ?', [userId]);
}

async function findIdsByUserId(userId) {
  const rows = await db.all('SELECT id FROM enrollments WHERE user_id = ?', [
    userId,
  ]);
  return rows.map((r) => r.id);
}

module.exports = {
  create,
  findByCourseId,
  deleteByUserId,
  findIdsByUserId,
};
