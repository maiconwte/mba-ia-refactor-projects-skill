const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');

let db;
let readyPromise;

function hashPassword(pwd) {
  return crypto.createHash('sha256').update(pwd).digest('hex');
}

function getDb() {
  if (!db) {
    throw new Error('Database not initialized. Call initDb() first.');
  }
  return db;
}

function run(sql, params = []) {
  return new Promise((resolve, reject) => {
    getDb().run(sql, params, function onRun(err) {
      if (err) reject(err);
      else resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
}

function get(sql, params = []) {
  return new Promise((resolve, reject) => {
    getDb().get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
}

function all(sql, params = []) {
  return new Promise((resolve, reject) => {
    getDb().all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
}

function initDb() {
  if (readyPromise) return readyPromise;

  readyPromise = new Promise((resolve, reject) => {
    db = new sqlite3.Database(':memory:');

    db.serialize(() => {
      db.run(
        'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)'
      );
      db.run(
        'CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)'
      );
      db.run(
        'CREATE TABLE enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)'
      );
      db.run(
        'CREATE TABLE payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)'
      );
      db.run(
        'CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)'
      );

      const leonanPass = hashPassword('123');
      db.run(
        "INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', ?)",
        [leonanPass]
      );
      db.run(
        "INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1), ('Docker', 497.00, 1)"
      );
      db.run('INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)');
      db.run(
        "INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')",
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  });

  return readyPromise;
}

function whenReady() {
  return readyPromise || initDb();
}

module.exports = {
  initDb,
  whenReady,
  run,
  get,
  all,
  hashPassword,
};
