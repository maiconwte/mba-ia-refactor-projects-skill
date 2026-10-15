const db = require('./database');

async function findByEmail(email) {
  return db.get('SELECT id, name, email, pass FROM users WHERE email = ?', [email]);
}

async function findById(id) {
  return db.get('SELECT id, name, email FROM users WHERE id = ?', [id]);
}

async function create(name, email, passHash) {
  const result = await db.run(
    'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
    [name, email, passHash]
  );
  return result.lastID;
}

async function deleteById(id) {
  return db.run('DELETE FROM users WHERE id = ?', [id]);
}

module.exports = {
  findByEmail,
  findById,
  create,
  deleteById,
};
