// composant for Result Empty
function ResultEmpty() {
  return (
    <div className="result-empty" style={{ marginTop: "5em" }}>
      <h2>No Results Found</h2>
      <p>Sorry, we couldn't find any results for your search.</p>
      <p>Please try a different search term or check your spelling.</p>
      <a href="/">Go to Home</a>
    </div>
  );
}

export default ResultEmpty;
