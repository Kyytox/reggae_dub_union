import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";

function SectionPagination({ nbPages, clickChangePage }) {
  return (
    <Stack spacing={2}>
      <Pagination
        count={nbPages}
        variant="outlined"
        shape="rounded"
        onChange={(event, value) => clickChangePage(value)}
      />
    </Stack>
  );
}

export default SectionPagination;
