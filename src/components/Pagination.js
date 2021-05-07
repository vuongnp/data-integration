import React from "react";
import { Pagination } from "@material-ui/lab";

import "./Pagination.css"

export default function Paging() {
  return (
    <div className="contain-paging">
      <Pagination count={10} variant="outlined" shape="rounded" className="paging" color="secondary"/>
    </div>
  );
}
