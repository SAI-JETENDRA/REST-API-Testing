import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore, doc, setDoc, arrayUnion } from "firebase/firestore"; 
import { getStorage, ref, uploadBytes } from "firebase/storage";


// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB3_fhKyJrWhjvxtIP1uwa8szWbCvladJ4",
  authDomain: "wired-apex-428407-u9.firebaseapp.com",
  projectId: "wired-apex-428407-u9",
  storageBucket: "wired-apex-428407-u9.appspot.com",
  messagingSenderId: "960986860185",
  appId: "1:960986860185:web:842823b5426eb1c65b8608",
  measurementId: "G-ZVT6GH5VXZ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app); // Initialize Firebase Storage

export { app, auth, db, doc, setDoc, arrayUnion, storage,ref, uploadBytes };
