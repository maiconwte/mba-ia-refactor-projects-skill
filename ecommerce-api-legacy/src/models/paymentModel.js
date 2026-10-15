const db = require('./database');

async function create(enrollmentId, amount, status) {
  return db.run(
    'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
    [enrollmentId, amount, status]
  );
}

async function findByEnrollmentId(enrollmentId) {
  return db.get(
    'SELECT amount, status FROM payments WHERE enrollment_id = ?',
    [enrollmentId]
  );
}

async function deleteByEnrollmentIds(enrollmentIds) {
  if (enrollmentIds.length === 0) return { changes: 0 };
  const placeholders = enrollmentIds.map(() => '?').join(',');
  return db.run(
    `DELETE FROM payments WHERE enrollment_id IN (${placeholders})`,
    enrollmentIds
  );
}

module.exports = {
  create,
  findByEnrollmentId,
  deleteByEnrollmentIds,
};
