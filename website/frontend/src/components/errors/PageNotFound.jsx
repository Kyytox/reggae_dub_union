// composant for Search not found
function PageNotFound() {
  return (
    <div className="page-not-found" style={{ marginTop: "5em" }}>
      <h2>Page Not Found</h2>
      <p>Sorry, the page you are looking for does not exist.</p>
      <p>Please check the URL or return to the home page.</p>
      <a href="/">Go to Home</a>
    </div>
  );
}

export default PageNotFound;
