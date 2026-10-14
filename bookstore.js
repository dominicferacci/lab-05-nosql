// Step 2: use bookstore (switch databases inside a script)
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
let authorDocs = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(authorDocs)

// Step 4: load books.json
db.books.drop()
let bookDocs = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(bookDocs)

// Step 5: list authors and books
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
db.books.insertMany([
  { title: "Fuzzy Mud", published_year: 2015, author_ids: ["author_004"] },
  { title: "The Hunger Games", published_year: 2008, author_ids: ["author_005"] }
])

// Step 7: add missing authors 
db.authors.insertMany([
  {
    _id: "author_004",
    name: "Louis Sachar",
    nationality: "American",
    bio: {
      short: "American author of children's and young adult fiction.",
      long: "Louis Sachar is an American novelist best known for Holes, which won the Newbery Medal and the National Book Award. He is also the author of the Wayside School series and Fuzzy Mud, a 2015 novel about a dangerous experiment gone wrong."
    }
  },
  {
    _id: "author_005",
    name: "Suzanne Collins",
    nationality: "American",
    bio: {
      short: "American author and television writer.",
      long: "Suzanne Collins is an American author and former television writer for children's programming. She is best known for The Hunger Games trilogy, a dystopian young adult series set in the nation of Panem, as well as the Underland Chronicles."
    }
  }
])

// Step 8: filter books by a list of authors 
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray())
