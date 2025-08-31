import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";

function SectionPagination({ nbPages, clickChangePage }) {
  return (
    <Stack spacing={5} sx={{ alignItems: "center", mb: 5, mt: 6 }}>
      <Pagination
        count={nbPages}
        variant="outlined"
        shape="rounded"
        color="primary"
        onChange={(event, value) => clickChangePage(value)}
      />
    </Stack>
  );
}

export default SectionPagination;
