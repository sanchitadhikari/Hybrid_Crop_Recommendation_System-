const USERS_KEY = "crop_users";
const SESSION_KEY = "crop_session_user";

export const DEMO_CREDENTIALS = {
  email: "demo@cropai.com",
  password: "Demo@123",
};

const DEMO_USER = {
  id: "demo-user",
  name: "Demo Farmer",
  email: DEMO_CREDENTIALS.email,
  password: DEMO_CREDENTIALS.password,
};

function getUsers() {
  const raw = localStorage.getItem(USERS_KEY);
  if (!raw) {
    saveUsers([DEMO_USER]);
    return [DEMO_USER];
  }
  try {
    const users = JSON.parse(raw);
    const hasDemo = users.some((u) => u.email.toLowerCase() === DEMO_USER.email.toLowerCase());
    if (!hasDemo) {
      users.push(DEMO_USER);
      saveUsers(users);
    }
    return users;
  } catch {
    saveUsers([DEMO_USER]);
    return [DEMO_USER];
  }
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

export function signupUser({ name, email, password }) {
  const users = getUsers();
  const exists = users.some((u) => u.email.toLowerCase() === email.toLowerCase());
  if (exists) {
    throw new Error("Email is already registered.");
  }

  const nextUser = {
    id: Date.now().toString(),
    name: name.trim(),
    email: email.trim(),
    password,
  };

  users.push(nextUser);
  saveUsers(users);
  localStorage.setItem(SESSION_KEY, JSON.stringify({ id: nextUser.id, name: nextUser.name, email: nextUser.email }));

  return nextUser;
}

export function loginUser({ email, password }) {
  const users = getUsers();
  const found = users.find((u) => u.email.toLowerCase() === email.toLowerCase());
  if (!found || found.password !== password) {
    throw new Error("Invalid email or password.");
  }

  const sessionUser = { id: found.id, name: found.name, email: found.email };
  localStorage.setItem(SESSION_KEY, JSON.stringify(sessionUser));
  return sessionUser;
}

export function getSessionUser() {
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function logoutUser() {
  localStorage.removeItem(SESSION_KEY);
}
